

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c e)
(on d a)
(on e d)
(clear c)
)
(:goal
(and
(on a d)
(on b a)
(on c e)
(on e b))
)
)


