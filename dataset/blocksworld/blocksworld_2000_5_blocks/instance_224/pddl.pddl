

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(ontable d)
(on e b)
(clear c)
(clear e)
)
(:goal
(and
(on b d)
(on c e)
(on d c))
)
)


