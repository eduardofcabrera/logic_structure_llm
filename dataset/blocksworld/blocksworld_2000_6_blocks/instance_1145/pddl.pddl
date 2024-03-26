

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(on c d)
(ontable d)
(on e b)
(clear a)
)
(:goal
(and
(on b a)
(on c e)
(on d b)
(on e d))
)
)


