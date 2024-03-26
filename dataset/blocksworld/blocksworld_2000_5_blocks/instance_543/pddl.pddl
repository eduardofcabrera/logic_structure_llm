

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c e)
(on d a)
(on e b)
(clear c)
(clear d)
)
(:goal
(and
(on b c)
(on d e))
)
)


