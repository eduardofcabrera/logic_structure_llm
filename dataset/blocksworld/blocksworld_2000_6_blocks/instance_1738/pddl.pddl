

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b c)
(ontable c)
(ontable d)
(on e b)
(clear a)
(clear e)
)
(:goal
(and
(on c a)
(on d c)
(on e d))
)
)


