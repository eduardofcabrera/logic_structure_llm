

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c d)
(on d a)
(on e b)
(clear c)
(clear e)
)
(:goal
(and
(on a b)
(on c e)
(on d a))
)
)


